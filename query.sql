SELECT created_at, to_char(created_at, 'Mon DD, YYYY HH24:MI'), status
  FROM tweets
  WHERE status NOT LIKE '@%' AND status NOT LIKE 'RT%' AND status NOT LIKE '%http://%'
  ORDER BY created_at DESC

  --select * from pg_timezone_names 