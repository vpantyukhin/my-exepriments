import boto3
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3')
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