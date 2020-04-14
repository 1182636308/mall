from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = """
        更新订单状态
        回收订单
    """
    def add_arguments(self, parser):
        # 添加命令的参数
        parser.add_argument(
            '--all',
            action ='store_true',
            dest = 'all',
            default = False,
            help = '回收所有超时的订单'

        )
        parser.add_argument(
            '--one',
            action ='store',
            dest = 'one',
            default = False,
            help = '回收某个订单'

        )



    def handle(self, *args, **options):
        if options['all']:
            self.stdout.write("开始回收订单")
            # 业务逻辑
            self.stdout.write('------------')
            self.stdout.write('全部回收完成')
        elif options['one']:
            self.stdout.write('已回收编号为{0}订单'.format(options['one']))


        else:
            self.stderr.write('指令异常')