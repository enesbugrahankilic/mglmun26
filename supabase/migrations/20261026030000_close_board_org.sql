-- Divan ve organizasyon başvuruları kapandı: herkese açık form yalnızca delege başvurusu kabul eder.
drop policy if exists "public can apply" on public.applications;
create policy "public can apply" on public.applications
  for insert to anon, authenticated
  with check (status = 'pending' and admin_note is null and kind = 'delegate');
