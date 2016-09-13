#!/usr/bin/env python

import json
import re
import sys


class CallGraphGenerator():

    def __init__(self):

        if len(sys.argv) == 0:
            filename = 'package.json'
        else:
            filename = sys.argv[1]

        self.filenames = {'in': filename, 'out': None}
        self.data = None
        self.tasks = []
        self.alltasks = []
        self.npm_default_task_fillcolor = '#fff2be'

        # list of predefined tasks (from https://docs.npmjs.com/misc/scripts)
        self.npm_default_tasks = [
            'prepublish',
            'publish',
            'postpublish',
            'preinstall',
            'install',
            'postinstall',
            'preuninstall',
            'uninstall',
            'postuninstall',
            'preversion',
            'version',
            'postversion',
            'pretest',
            'test',
            'posttest',
            'prestop',
            'stop',
            'poststop',
            'prestart',
            'start',
            'poststart',
            'prerestart',
            'restart',
            'postrestart'
        ]

    def readfile(self):

        print('reading from: ' + self.filenames['in'])
        with open(self.filenames['in'], 'r') as fp:
            self.data = json.load(fp)

        id = 0
        for npm_default_task in self.npm_default_tasks:
            if npm_default_task not in self.data['scripts'].keys():
                d = {
                    'id': id,
                    'name': npm_default_task,
                    'content': None,
                    'dependencies': None
                }
                id += 1
                self.tasks.append(d)

        tasks = sorted(self.data['scripts'].items())
        for task in tasks:
            d = {
                'id': id,
                'name': task[0],
                'content': task[1],
                'dependencies': re.findall('npm run ([\S]*)', task[1])
            }
            id += 1
            self.tasks.append(d)


        for task in self.tasks:
            self.alltasks.append(task['name'])

    def writedot(self):
        self.filenames['out'] = self.data['name'] + '.dot'
        print('writing to: ' + self.filenames['out'])
        with open(self.filenames['out'], 'w') as fp:

            # write the opening sequence for *.dot files
            fp.write('digraph ' + self.data['name'] + '{\n')

            # write the list of nodes
            for task in self.tasks:

                properties = []

                # add the name of the node
                properties.append('label="' + task['name'] + '"')

                # add the raw code for the task if you have it
                if task['content'] is not None:
                    properties.append('tooltip="' + task['content'] + '"')

                # use a different fillcolor for npm default tasks
                if task['name'] in self.npm_default_tasks:
                    properties.append('fillcolor="' + self.npm_default_task_fillcolor + '"')
                    properties.append('style="filled"')

                # concatenate properties into a comma-separated string
                propstr = ', '.join(properties)

                fp.write(str(task['id']) + ' [' + propstr + ']\n')

            # write the list of edges from one task to another
            for task in self.tasks:
                if task['dependencies'] is not None:
                    for depname in task['dependencies']:
                        depid = [item['id'] for item in self.tasks if item["name"] == depname]
                        fp.write(str(task['id']) + ' -> ' + str(depid[0]) + '\n')

            # write the list of edges that include post- or pre- tasks
            # if the taskname starts with pre<something> OR ppost<something> AND there
            # is another task called <something>, which might be a nodejs default task, link
            # the two together
            for task in self.tasks:
                if re.findall('^pre.*', task['name']):
                    depname = task['name'][3:]
                    if depname in self.alltasks:
                        # task's name is 'pre<something>' and <something> exists
                        depid = [item['id'] for item in self.tasks if item["name"] == depname]
                        #fp.write(str(task['id']) + ' -> ' + str(depid[0]) + '\n')
                        fp.write(str(depid[0]) + ' -> ' + str(task['id']) + '\n')

                if re.findall('^post.*', task['name']):
                    depname = task['name'][4:]
                    if depname in self.alltasks:
                        # task's name is 'post<something>' and <something> exists
                        depid = [item['id'] for item in self.tasks if item["name"] == depname]
                        fp.write(str(depid[0]) + ' -> ' + str(task['id']) + '\n')
                        #fp.write(str(task['id']) + ' -> ' + str(depid[0]) + '\n')

            # write the closing sequence for *.dot files
            fp.write('}\n')

if __name__ == '__main__':

    cgg = CallGraphGenerator()
    cgg.readfile()
    cgg.writedot()


