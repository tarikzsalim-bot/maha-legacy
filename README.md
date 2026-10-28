# بصمة وفاء — المعلمة مها حلواني

موقع عربي بتصميم كحلي وذهبي، يعرض رسالة المعلمة ومسيرتها وجدار بصمات عامًّا، ويتيح إرسال رسالة دون تسجيل دخول مع اعتمادها قبل النشر.

## النشر على GitHub Pages
1. أنشئ مستودعًا عامًا على GitHub وارفع `index.html`.
2. من Settings → Pages اختر Deploy from a branch ثم `main` و`/(root)`.
3. انتظر ظهور رابط الموقع في صفحة Pages.

## تفعيل التعليقات المشتركة
1. أنشئ مشروعًا في Supabase.
2. نفّذ `schema.sql` في SQL Editor.
3. من Project Settings / API انسخ Project URL و **anon/publishable key** فقط (لا تستخدم service_role أو secret key مطلقًا في الموقع).
4. في `index.html` عدّل `SUPABASE_URL` و`SUPABASE_ANON_KEY` ثم ارفع التعديل.
5. راجع التعليقات من Supabase → Table Editor → guestbook، وغيّر `approved` إلى `true` للرسائل المقبولة.

**مهم:** بدون إعداد Supabase، الموقع يعمل كواجهة عرض لكن لا يستقبل أو يعرض تعليقات مشتركة. سياسات RLS تمنع الزوار من رؤية الرسائل غير المعتمدة أو اعتمادها بأنفسهم. للنشر العام طويل الأمد، أضف CAPTCHA وتحديد معدل الطلبات عبر وظيفة خادم.
