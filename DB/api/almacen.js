import {addAlmacen,getAlmacen,delArticulo} from "../funciones/almacen.js"
import {cors} from "../funciones/cors.js"
export default function handler(req,res){
    cors(req,res)
     
    if(req.method === "POST"){
       
      if(parseInt(req.headers["id"]) === 0)
      {

          return addAlmacen(req,res)
      }
      return delArticulo(req,res)
    }
   return getAlmacen(req,res)
   
}