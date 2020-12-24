


const auth_session_url = 'http://127.0.0.1:9090/login';




const form = document.querySelector('form');
const formEvent = form.addEventListener('submit', async event => {
    event.preventDefault();
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    const credential = { username, password };
    authenticate = authentication(credential);
   
    
 });



const authentication = async credential => {
    try {
         const response = await axios.post(`${auth_session_url}`, credential);
         const auth_response = response.data;
         console.log(auth_response);

         
     } 
     catch (e) {
            console.error(e);
     }
 };



// function to set cookie
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
