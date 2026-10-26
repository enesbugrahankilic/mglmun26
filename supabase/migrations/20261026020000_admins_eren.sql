-- Eren'in admin hesabı erenmglmun26@gmail.com ile açıldı
insert into public.admins (email) values ('erenmglmun26@gmail.com')
on conflict (email) do nothing;
delete from public.admins where email = 'erendg@gmail.com';
