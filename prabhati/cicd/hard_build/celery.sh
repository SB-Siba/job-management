
sudo apt-get install redis-server
echo "redis install done"

sudo apt-get install supervisor
echo "supervisor install done"

cd /var/lib/jenkins/workspace/hvproject/cicd/hard_build/

sudo cp -r celery_worker.conf /etc/supervisor/conf.d/

echo "some more commands"

sudo systemctl status supervisor

sudo supervisorctl update
sudo supervisorctl restart celery-default
sudo supervisorctl status celery-default