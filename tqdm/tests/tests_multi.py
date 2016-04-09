from tqdm import tqdm, multi_tqdm, tqdm_job
from tests_tqdm import with_setup, pretest, posttest, StringIO, closing

@with_setup(pretest, posttest)
def test_multi():
    """ Test multi_tqdm with test tqdm_job """
    class TestJob(tqdm_job):

        def __init__(self, task_num, **kwargs):
            super(TestJob, self).__init__(**kwargs)
            self.task_num = task_num

        def update(self):
            self.pbar.update(self.task_num)

        def handle_result(self, out):
            if self.task_num == 5:
                raise NameError('No 5s allowed')
            else:
                return 'Success: {self.task_num}\n'.format(self=self)

        def success_callback(self, result, out):
            out.write(result)

        def failure_callback(self, error, out):
            out.write('Failed {self.task_num} with error: "{error}"\n'.format(self=self, error=error))

    with closing(StringIO()) as our_file, closing(StringIO()) as output:
        multi = multi_tqdm()
        for task_num in range(1, 10):
            job = TestJob(task_num=task_num, file=our_file, desc=str(task_num), total=1000)
            multi.register_job(job)
        with open('results.txt', 'w') as out2:
            multi.run(sleep_delay=.001, out=out2)
