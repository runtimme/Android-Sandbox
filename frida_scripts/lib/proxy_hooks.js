function bypass_ssl_pinning(){
    var array_list = Java.use("java.util.ArrayList");
    var ApiClient = Java.use('com.android.org.conscrypt.TrustManagerImpl');

    ApiClient.checkTrustedRecursive.implementation = function(a1,a2,a3,a4,a5,a6) {
            var k = array_list.$new();
            return k;
    }
}

exports.bypass_ssl_pinning = bypass_ssl_pinning