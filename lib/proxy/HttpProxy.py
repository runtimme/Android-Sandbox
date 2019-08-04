from mitmproxy import ctx

class Addon():

    def request(self, flow):
        '''
        Addon used by mitmproxy that store each url in a file
        :param flow:
        :return:
        '''
        url_b = flow.request.url

        with open("tmp/urls.txt","a") as f:
            ctx.log.info(f"Writing url : {url_b}")
            f.write(url_b +'\n')

    def response(self, flow):
        pass

addons = [
    Addon()
]