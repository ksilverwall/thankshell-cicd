import os
import argparse
import subprocess
import json

BUCKET_NAME = 'com-thankshell-work'

ENV_PARAMS = {
    'production': {
        'DeployBucket': 'production-thankshell-react',
        'Distribution': 'EC625W0BJ2K3B',
        'StackName': 'thankshell-release-production',
    },
    'staging': {
        'DeployBucket': 'staging-thankshell-react',
        'Distribution': 'EWED4ZETHFRQF',
        'StackName': 'thankshell-release-staging',
    },
}

def deploy(env, secrets):
    config = ENV_PARAMS[env] 

    subprocess.run([
        'sam', 'package',
        '--output-template-file', 'packaged.yaml',
        '--s3-bucket', BUCKET_NAME,
    ])

    subprocess.run([
        'sam', 'deploy',
        '--template-file', 'packaged.yaml',
        '--stack-name', config['StackName'],
        '--capabilities', 'CAPABILITY_IAM',
        '--parameter-overrides',
        'GitHubToken={}'.format(secrets['GithubToken']),
        'DeployBucket={}'.format(config['DeployBucket']),
        'Distribution={}'.format(config['Distribution']),
    ])

if __name__ == '__main__':
    os.chdir(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', '--environment',
        choices=ENV_PARAMS.keys(),
        default='staging',
    )
    args = parser.parse_args()

    deploy(args.environment, json.load(open('secrets.json')))
