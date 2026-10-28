-- Run in Supabase SQL Editor. Only approved messages are public.
create table if not exists public.guestbook (
 id bigint generated always as identity primary key,
 name text not null check (char_length(name) between 1 and 70),
 relation text not null check (relation in ('طالبة','زميلة','إدارية','ولية أمر','أخرى')),
 message text not null check (char_length(message) between 1 and 1200),
 approved boolean not null default false,
 created_at timestamptz not null default now()
);
alter table public.guestbook enable row level security;
create policy "Public can read approved messages" on public.guestbook for select to anon using (approved = true);
create policy "Visitors can submit pending messages" on public.guestbook for insert to anon with check (approved = false);
-- Review and approve submissions using the Supabase dashboard (Table Editor).
-- For production, enable CAPTCHA / rate limiting through an Edge Function to reduce spam.
