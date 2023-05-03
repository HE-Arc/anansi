import { defineStore } from 'pinia';

export const useToolsStore = defineStore('tools', () =>{
  function readCookie(name: string) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for(let i=0;i < ca.length;i++) {
      let c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1,c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
  }

  function rmExcessSpaces(text: any) {
      text = text.split(" ");
      text.forEach((word:any, index:any) => {
        if (word === "") {
          text.splice(index, 1);
        }
      });
      const index = text.length;
      text = text.join(" ");
      return index;
    }

    function clozeCardText(text:string, index:number) {
      const words = text.split(" ");
      return words.slice(0, index).join(" ") + " __________ " + words.slice(index).join(" ");
    };

  function validationErrors(error: any) {
    const errors = [];
    for (const key in error) {
      for (const key2 in error[key]) {
        errors.push(key + " : " + error[key][key2]);
      }
    }
    return errors;
  }

  return { readCookie, rmExcessSpaces, validationErrors, clozeCardText };
});
