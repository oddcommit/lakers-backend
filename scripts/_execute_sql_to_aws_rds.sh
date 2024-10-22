#!/bin/bash -e

set -e

# scripts配下に.sqlファイルがない場合は終了
sql_file_count=$(find scripts -type f -name "*.sql" -o -name "*.csv" | wc -l)
if ! [ "$sql_file_count" -gt 0 ]; then
    echo "scripts配下に.sqlファイルまたは.csvがありません"
    exit 1
fi

# 踏み台サーバーに接続していない場合は終了
if ! lsof -i :9999 >/dev/null; then
    echo -e "踏み台サーバーに接続していません\nbastion-ec2コマンドを実行してください"
    exit 1
fi

# AWS_PROFILEが設定されていない場合は終了
if [ -z "${AWS_PROFILE}" ]; then
    echo -e "***AWS_PROFILEが設定されていません***\naws-al○を行ってください\n○は環境に応じて変更"
    exit 1
fi

echo -e "AWS_PROFILEの値は「${AWS_PROFILE}」です"

export DB_NAME=$(aws ssm get-parameter --name /lakers-saas/backend/db-name --with-decryption --query Parameter.Value --output text)
export DB_USER=$(aws ssm get-parameter --name /lakers-saas/backend/db-user --with-decryption --query Parameter.Value --output text)
export PGPASSWORD=$(aws ssm get-parameter --name /lakers-saas/backend/db-password --with-decryption --query Parameter.Value --output text)

echo "台帳CSVをLoadします"
csv_files="./scripts/*.csv"
PY_OPT="--pref ${@:1:1}"
YEAR=${@:2:1}
re='^20[0-9]{2}$'
if [[ $YEAR =~ $re ]] ; then
   PY_OPT="${PY_OPT} --year ${YEAR}"
fi

for csv_path in $csv_files; do
    [[ -f "$csv_path" ]] || continue
    echo "${csv_path}の処理を開始します"
    poetry run python manage.py load_book_csv --csv ${csv_path} $PY_OPT
    echo "${csv_path}の処理が完了しました"
done

sql_file_directory="./scripts/*.sql"
for sql_file_path in $sql_file_directory; do
    [[ -f "$sql_file_path" ]] || continue
    echo "${sql_file_path}の処理を開始します"

    psql --host localhost \
         --port 9999 \
         --username ${DB_USER} \
         --dbname ${DB_NAME} \
         --file "${sql_file_path}" \
         --single-transaction\
         --set ON_ERROR_STOP=on

    echo "${sql_file_path}の処理が完了しました"
done

exit 0