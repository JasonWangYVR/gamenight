# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"

cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end

cookbook_file "rc.local" do
  path "/etc/rc.local"
end

execute 'ntp_restart' do
  command 'service ntp restart'
end

#nginx
package "nginx"
cookbook_file "nginx-default" do
    path "etc/nginx/sites-available/default"
end

cookbook_file "uwsgi_params" do
    path "etc/nginx/uwsgi_params"
end
service "nginx" do
    action :restart
end

#Postgres
package "postgresql"
execute 'postgres_user' do
    command 'echo "CREATE DATABASE mydb; CREATE USER ubuntu; GRANT ALL PRIVILEGES ON DATABASE mydb TO ubuntu;" | sudo -u postgres psql';
end

#django deployment mode
package "postgresql-server-dev-all"
package "python-pip"
package "libpython-dev"
execute 'django_install' do
	command 'pip install django'
end
execute 'psycopg2_install' do
    command 'pip install psycopg2'
end
execute 'uwsgi_install' do
    command 'pip install uwsgi'
end
execute 'pillow_install' do
  command 'pip install Pillow'
end
execute 'captcha_install' do
    command 'pip install django-simple-captcha'
end
execute 'make_migrations' do
    user 'ubuntu'
    cwd '/home/ubuntu/project/gamenight'
    command 'python manage.py makemigrations'
end
execute 'db_migration' do
	user 'ubuntu'
	cwd '/home/ubuntu/project/gamenight/'
	command 'python manage.py migrate'
end

execute 'load_bgdata' do
	user 'ubuntu'
	cwd 'home/ubuntu/project/gamenight/'
	command 'python manage.py loaddata bg_data.json'
end

execute 'static_files' do
  user 'ubuntu'
  cwd 'home/ubuntu/project/gamenight'
  command 'python manage.py collectstatic --noinput'
end

execute 'startup' do
    command '/etc/rc.local'
  end
