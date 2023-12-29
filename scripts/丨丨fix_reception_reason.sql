-- 所有権移転相続法人合併 → 所有権移転相続・法人合併
update product.public.data_models_realestatereceptionbook
set reception_reason = '所有権移転相続・法人合併'
where reception_reason = '所有権移転相続法人合併';

-- 所有権移転遺贈贈与その他無償名義 → 所有権移転遺贈・贈与その他無償名義
update product.public.data_models_realestatereceptionbook
set reception_reason = '所有権移転遺贈・贈与その他無償名義'
where reception_reason = '所有権移転遺贈贈与その他無償名義';

-- 登記名義人の氏名等についての変更更正 → 登記名義人の氏名等についての変更・更正
update product.public.data_models_realestatereceptionbook
set reception_reason = '登記名義人の氏名等についての変更・更正'
where reception_reason = '登記名義人の氏名等についての変更更正';

-- 権利の変更更正 → 権利の変更・更正
update product.public.data_models_realestatereceptionbook
set reception_reason = '権利の変更・更正'
where reception_reason = '権利の変更更正';

-- 敷地権の表示の登記の変更更正 → 敷地権の表示の登記の変更・更正
update product.public.data_models_realestatereceptionbook
set reception_reason = '敷地権の表示の登記の変更・更正'
where reception_reason = '敷地権の表示の登記の変更更正';

-- 床面積の変更更正 → 床面積の変更・更正
update product.public.data_models_realestatereceptionbook
set reception_reason = '床面積の変更・更正'
where reception_reason = '床面積の変更更正';

-- 地目変更更正 → 地目変更・更正
update product.public.data_models_realestatereceptionbook
set reception_reason = '地目変更・更正'
where reception_reason = '地目変更更正';

-- 地積変更更正 → 地積変更・更正
update product.public.data_models_realestatereceptionbook
set reception_reason = '地積変更・更正'
where reception_reason = '地積変更更正';

-- 分割区分 → 分割・区分
update product.public.data_models_realestatereceptionbook
set reception_reason = '分割・区分'
where reception_reason = '分割区分';

-- 減失→滅失
update product.public.data_models_realestatereceptionbook
set reception_reason = '滅失'
where reception_reason = '減失';

-- 権利の移転所有権を除く → 権利の移転(所有権を除く)
update product.public.data_models_realestatereceptionbook
set reception_reason = '権利の移転(所有権を除く)'
where reception_reason = '権利の移転所有権を除く';

-- 所有権の保存申請 → 所有権の保存（申請）
update product.public.data_models_realestatereceptionbook
set reception_reason = '所有権の保存(申請)'
where reception_reason = '所有権の保存申請';

-- 仮登記所有権 → 仮登記(所有権)
update product.public.data_models_realestatereceptionbook
set reception_reason = '仮登記(所有権)'
where reception_reason = '仮登記所有権';

-- 仮登記その他 → 仮登記(その他)
update product.public.data_models_realestatereceptionbook
set reception_reason = '仮登記(その他)'
where reception_reason = '仮登記その他';

-- かっこの半角統一
UPDATE data_models_realestatereceptionbook
SET reception_reason = REPLACE(reception_reason, '（', '(');

UPDATE data_models_realestatereceptionbook
SET reception_reason = REPLACE(reception_reason, '）', ')');

--  末尾の/削除
UPDATE data_models_realestatereceptionbook
SET reception_reason = TRIM(TRAILING '/' From reception_reason);

UPDATE data_models_realestatereceptionbook
SET reception_reason = TRIM(TRAILING '／' From reception_reason);