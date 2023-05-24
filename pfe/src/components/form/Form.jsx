import React, { useState } from "react";
import { Stepper, Step, StepLabel } from '@material-ui/core';
import './form.css';
import Swal from 'sweetalert2';
import axios from 'axios';
import CryptoJS from 'crypto-js';




const Form = ({ data }) => {
  const sectionNames = data.map((section) => section.name);
  const [formValues, setFormValues] = useState({});
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [currentFieldIndex, setCurrentFieldIndex] = useState(0);
  const [inputValue, setInputValue] = useState("");
  const [isFormValid, setIsFormValid] = useState(true);


  const handleSubmit = (event) => {
    event.preventDefault();
  const isFormValid = checkFormValidity();
  setIsFormValid(isFormValid);
  if (isFormValid) {
    const hasEmptyFields = Object.values(formValues).every(value => {value.trim() !== ''});
    console.log(hasEmptyFields)

    if (hasEmptyFields) {
      Swal.fire({
        title: 'Error!',
        text: 'One or more fields are empty',
        icon: 'error',
        confirmButtonText: 'OK'
      });
      return '';
    }
    
    console.log("formValues:", JSON.stringify(formValues));
    axios
    .post('http://127.0.0.1:5000/form', { data: formValues })
  

      .then((response) => {
        //setOutputLink(URL.createObjectURL(new Blob([response.data])));
       window.open(response.data.url) 
      })
    
      .catch((error) => {
        console.error("Error:", error);
      })
    
  };}

  const toBase64 = (file) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });

  

  const handleInputChange = (event, id) => {
    setFormValues({ ...formValues, [id]: event.target.value });
  };

  const handleNext = () => {
    const nextSectionIndex = currentSectionIndex + 1;
    if (nextSectionIndex < data.length) {
      setCurrentSectionIndex(nextSectionIndex);
      setCurrentFieldIndex(0);
    }
    console.log(formValues);
  };

  const handlePrevious = () => {
    const currentSection = data[currentSectionIndex];
    const previousFieldIndex = currentFieldIndex - 1;
    if (previousFieldIndex >= 0) {
      setCurrentFieldIndex(previousFieldIndex);
    } else {
      const previousSectionIndex = currentSectionIndex - 1;
      if (previousSectionIndex >= 0) {
        setCurrentSectionIndex(previousSectionIndex);
        const previousSection = data[previousSectionIndex];
        setCurrentFieldIndex(previousSection.fields.length - 1);
      }
    }
  };

  const checkFormValidity = () => {
    // Check form validity here
    return true;
  };

return (
<div className="aa">
  <div className="a3">
  <nav className="a1">
     <Stepper style={{ backgroundColor:"transparent"
      }}
      activeStep={currentSectionIndex} alternativeLabel>
        {sectionNames.map((name) => (
          <Step key={name}>
            <StepLabel >{name}</StepLabel>
          </Step>
        ))}
    </Stepper>
  </nav>
  
  <div className="a2"> 
<form onSubmit={handleSubmit} >
{data.map((section, sectionIndex) => (
<div key={section.name} style={{ display: currentSectionIndex === sectionIndex ? "block" : "none" }} ><br></br>
<h2 >{section.name}</h2><br></br>
<div className="container">
          {section.ids.map((field) => (
            <div key={field.lines} >
              {field.fieldType === "Text" && (
                <label className="input-field">
                  {field.lines}:
                  <input
                    type="text"
                    value={formValues[field.lines] || ""}
                    required={true}
                    placeholder= {field.lines}
                    onChange={(event) => handleInputChange(event, field.lines)}
                  />
                </label>
              )}
              {field.fieldType === "Image" && (
               <label>
                {field.lines}:
                <input
                type="file"
                accept="image/*"
                onChange={async (event) => {
                const file = event.target.files[0];
                const base64 = await toBase64(file);
                handleInputChange(base64, field.lines);
                }}
                required={true}
                />
               </label>
               )}
               
              {field.fieldType === "Check" && (
                <div>
                  <label className="input-field">
                    <input
                      type="checkbox"
                      checked={formValues[field.lines] || false}
                      required={true}
                      
                      onChange={(event) =>
                        handleInputChange(event, field.lines)
                      }
                    />
                    {field.lines}
                  </label>
                </div>
              )}
              {field.fieldType === "HTML" && (
                <div
                  dangerouslySetInnerHTML={{ __html: field.lines }}
                ></div>
              )}
              {field.fieldType === "Date" && (
                <label className="input-field">
                  {field.lines}:
                  <input
                    type="date"
                    value={formValues[field.lines] || ""}
                    required={true}
                    onChange={(event) => handleInputChange(event, field.lines)}
                  />
                </label>
              )}
              {field.fieldType === "Phone" && (
                <label className="input-field">
                  {field.lines}:
                  <input
                    type="tel"
                    value={formValues[field.lines] || ""}
                    required={true}
                    onChange={(event) => handleInputChange(event, field.lines)}
                  />
                </label>
              )}
              
              {field.fieldType === "BIC" && (
                <label className="input-field">
                  {field.lines}:
                  <input
                    type="string"
                    value={formValues[field.lines] || ""}
                    required={true}
                    placeholder= {field.lines}
                    onChange={(event) => handleInputChange(event, field.lines)}
                  />
                </label>
              )}
              {field.fieldType === "IBAN" && (
                <label className="input-field">
                  {field.lines}:
                  <input
                    type="string"
                    value={formValues[field.lines] || ""}
                    required={true}
                    placeholder= {field.lines}
                    onChange={(event) => handleInputChange(event, field.lines)}
                  />
                </label>
              )}
              {field.fieldType === "Numero" && (
                <label className="input-field">
                  {field.lines}:
                  <input
                    type="num"
                    value={formValues[field.lines] || ""}
                    required={true}
                    placeholder= {field.lines}
                    onChange={(event) => handleInputChange(event, field.lines)}
                  />
                </label>
              )}
              
              
              
            </div>
          ))}
           </div>
        </div>
      ))}
     
     <div className="button-container" style={{ display: 'flex', justifyContent: 'space-between' }}>
  <button className="prec" disabled={currentSectionIndex === 0 && currentFieldIndex === 0} onClick={handlePrevious}>
    Previous
  </button>
  {currentSectionIndex === data.length - 1 ? (
  <button type="submit" onClick={handleSubmit} className="next">
    Submit
  </button>
 ):(
  <button onClick={handleNext} className="next">
    Next
  </button>
)}
</div>
    </form>
    
    </div>
    </div>
    <form onSubmit={handleSubmit}>
 

</form>

    </div>
    
  
    
  );
};

export default Form;