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

  return { readCookie, rmExcessSpaces };
  /*id: "tools",
  actions: {
    readCookie(name: string) {
      const nameEQ = name + "=";
      const ca = document.cookie.split(';');
      for(let i=0;i < ca.length;i++) {
        let c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
      }
      return null;
    }
  }*/
});
