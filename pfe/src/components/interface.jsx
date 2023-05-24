import Navbar from '../components/navbar/Navbar';
import Form from "../components/form/Form";

import data from "../data.json";
function Interface() {
    return (
      <div>
        <Navbar  />
        <Form data={data} />
        
        
    
        
      </div>
    );
  }
  export default Interface