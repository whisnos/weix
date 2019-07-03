from application import app,manager
from flask_script import Server
import www
# 需要引入所有变量

# 可自定义命令
manager.add_command('run',Server(host='0.0.0.0',port=app.config['SERVER_PORT'],use_debugger=True))
def main():
	manager.run()


if __name__ == '__main__':
	try:
		import sys

		sys.exit(main())
	except Exception as e:
		import traceback

		traceback.print_exc()
