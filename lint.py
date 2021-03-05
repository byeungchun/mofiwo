"""Pylint output"""
from pylint import lint

run = lint.Run(['mofiwo', '--ignore=_version.py'], do_exit=False)
score = run.linter.stats['global_note']

print(f'##vso[task.setvariable variable=mofiwo.pylint_score]{score}')

f = open("codequality_reports/pylint_report.txt", "w")
f.write(f'Your code has been rated at {score}/10')
f.close()
