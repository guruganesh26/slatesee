import os
import io
import uuid
import logging

from slatese.settings import EVENTS_GALLERY_PATH, PROFILE_IMAGE_PATH


def remove_uploaded_file(file_path):
    if os.path.exists(file_path) :
        os.remove(file_path)


def convert_base64_to_file(file_name, file_content, school_id, is_profile):
    if file_content is not None:
        if is_profile:
            school_directory = "%s/%s" % (PROFILE_IMAGE_PATH, school_id)
        else:
            school_directory = "%s/%s" % (EVENTS_GALLERY_PATH, school_id)
        
        file_path = "%s/%s" % (school_directory, file_name)
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
            from google.appengine.api import app_identity
            bucket_name = os.environ.get(school_directory,
                                     app_identity.get_default_gcs_bucket_name())
            file_path = "/%s%s" % (bucket_name, file_path)
            create_file(file_path, file_content.decode('base64'))
        else:
            school_directory = '../'+school_directory
            if not os.path.exists(school_directory):
                os.makedirs(school_directory)
            #remove_uploaded_file(file_path)
            with io.FileIO('../'+file_path, "wb") as fn:
                fn.write(file_content.decode('base64'))

        return file_path
    return None

def new_uuid() :
        s = str(uuid.uuid4())
        return s.replace("-", "")


#[START write]
def create_file(filename, content):
    """Create a file.

    The retry_params specified in the open call will override the default
    retry params for this particular file handle.

    Args:
      filename: filename.
    """
    logging.info('filename' + filename)
    import cloudstorage as gcs
    from google.appengine.api import app_identity

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar',
                                 'x-goog-acl': 'public-read'},
                        retry_params=write_retry_params)
    gcs_file.write(content)
    gcs_file.close()
#[END write]

#[START read]
def read_file(self, filename):
    import cloudstorage as gcs
    from google.appengine.api import app_identity

    gcs_file = gcs.open(filename)
    gcs_file.seek(-1024, os.SEEK_END)
    gcs_file.close()
#[END read]
