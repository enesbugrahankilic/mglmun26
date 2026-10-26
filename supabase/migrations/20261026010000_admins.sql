-- Admin panelini görebilecek e-postalar
insert into public.admins (email) values
  ('erendg@gmail.com'),
  ('enesusg@gmail.com')
on conflict (email) do nothing;
