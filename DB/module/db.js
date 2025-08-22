import sqlite3 from "sqlite3"
import { open } from 'sqlite';
import path from "path"
sqlite3.verbose()
export const database = async () => {
    
    const new_path = path.join(path.resolve(),"/DataBase/Datos.db")
   
    try {
       const  db = await open({filename:new_path,driver:sqlite3.Database})
      
        return { ok: true, connection:db  }

    } catch (err) {
        console.log(err)
        return { ok: false, res: err }
    }
}
