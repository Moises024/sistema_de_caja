import {cors} from "../funciones/cors.js"
import { addInventario,getInventario,delInventario, getInventarioUsuario } from "../funciones/inventario.js"

 export default function handler(req,res){
    cors(req,res)
    if(req.method === "POST"){
        if(parseInt(req.headers["id"]) === 0)
        {
            return addInventario(req,res)
        }
        if(parseInt(req.headers["id"]) === 1)
        {
            return delInventario(req,res)
        }
         if(parseInt(req.headers["id"])=== 4){
        return getInventarioUsuario(req,res) 
    }

        return
    }
   
 return getInventario(req,res) 
 }
