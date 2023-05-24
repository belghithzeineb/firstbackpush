import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import './footer.css'



function footer() {
    return (
        <div className="footer"> 
   <footer class="footer-distributed">

<div class="footer-left">

    <h3>Con<span>tact</span></h3>

    

    <p class="footer-company-name">Lloyd © 2023</p>

    

</div>

<div class="footer-right">

    <p>Contact Us</p>

    <form action="#" method="post">

        <input type="text" name="email" placeholder="Email"/>
        <textarea name="message" placeholder="Message"></textarea>
        <button>Send</button>

    </form>

</div>

</footer>
  </div>
    );
  }
  
  export default footer;