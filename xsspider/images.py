from scrapy.contrib.pipeline.images import ImagesPipeline
import hashlib
from datetime import datetime

class MyImagesPipeline(ImagesPipeline):
    """
    def file_path(self, url):
        image_guid = hashlib.sha1(url).hexdigest()
        #return 'full/%s.jpg' % (image_guid)
        path = datetime.now().strftime("%Y/%m/%d")
        return '%s/%s.jpg' % (path, image_guid)
    """   
        

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        image_guid = hashlib.sha1(url).hexdigest()  # change to request.url after deprecation
        path = datetime.now().strftime("%Y/%m/%d")
        print path,"\n"
        return '%s/%s.jpg' % ('full', image_guid)

