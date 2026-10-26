-- MGLMUN'26 — başvuru tablosu ve admin yetkisi
-- Supabase → SQL Editor → New query → bu dosyanın tamamını yapıştır → Run

create extension if not exists pgcrypto;

-- Admin olarak giriş yapabilecek e-postalar
create table if not exists public.admins (
  email text primary key
);

create table if not exists public.applications (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  kind text not null check (kind in ('delegate','board','org')),
  full_name text not null check (char_length(full_name) between 2 and 120),
  email text not null check (char_length(email) <= 200),
  phone text not null check (char_length(phone) <= 30),
  guardian_phone text not null check (char_length(guardian_phone) <= 30),
  school text not null check (char_length(school) <= 200),
  grade text not null check (char_length(grade) <= 30),
  role text check (char_length(role) <= 80),
  pref1 text, pref2 text, pref3 text,
  experience text not null check (char_length(experience) <= 3000),
  awards text not null check (char_length(awards) <= 1000),
  motivation text not null check (char_length(motivation) between 300 and 1500),
  diet text not null check (diet in ('No restriction','Vegetarian','Vegan','Halal','Other')),
  allergens text[] not null default '{}',
  diet_note text check (char_length(diet_note) <= 300),
  medical_note text check (char_length(medical_note) <= 300),
  kvkk boolean not null check (kvkk = true),
  share_ok boolean not null default false,
  media_ok boolean not null default false,
  status text not null default 'pending' check (status in ('pending','reviewed','accepted','rejected')),
  admin_note text
);

alter table public.applications enable row level security;
alter table public.admins enable row level security;

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.admins where lower(email) = lower(auth.jwt() ->> 'email'));
$$;

-- Herkes (giriş yapmadan) sadece yeni başvuru ekleyebilir; okuyamaz.
drop policy if exists "public can apply" on public.applications;
create policy "public can apply" on public.applications
  for insert to anon, authenticated
  with check (status = 'pending' and admin_note is null);

-- Sadece admins tablosundaki e-postalar okuyup güncelleyebilir.
drop policy if exists "admins read" on public.applications;
create policy "admins read" on public.applications
  for select to authenticated using (public.is_admin());

drop policy if exists "admins update" on public.applications;
create policy "admins update" on public.applications
  for update to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "admins see admins" on public.admins;
create policy "admins see admins" on public.admins
  for select to authenticated using (public.is_admin());

-- Admin e-postalarını buraya yaz (Authentication → Users'ta da aynı e-postayla kullanıcı oluştur)
-- insert into public.admins (email) values ('ornek@gmail.com');
