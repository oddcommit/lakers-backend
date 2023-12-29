#!/bin/bash -e

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
export DB_PASSWORD=$(aws ssm get-parameter --name /lakers-saas/backend/db-password --with-decryption --query Parameter.Value --output text)
export DB_PORT="9999"

echo -e "「${AWS_PROFILE}」のRDSの環境変数を設定しました"
