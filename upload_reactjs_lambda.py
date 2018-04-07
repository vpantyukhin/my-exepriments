import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:527104445792:DeployReactJStopic')
    
    try:
        targetbucket = s3.Bucket('reactjs.awspyc.com')
        
        buildbucket = s3.Bucket('reactjsbuild.awspyc.com')
        
        reactjs_zip = StringIO.StringIO()
        buildbucket.download_fileobj('reactjs.zip', reactjs_zip)
        
        with zipfile.ZipFile(reactjs_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                targetbucket.upload_fileobj(obj, nm,
                    ExtraArgs = {'ContentType': mimetypes.guess_type(nm)[0]})
                targetbucket.Object(nm).Acl().put(ACL='public-read')
        
        print "Job done"
        topic.publish(Subject='ReactJS', Message='NodeJS deployed Sucessfully')
    except:
        topic.publish(Subject='ReactJS', Message='NodeJS deployment Failed')
        raise
            
    return 'Hello from Lambda'
