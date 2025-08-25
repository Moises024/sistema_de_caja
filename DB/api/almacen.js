import { addAlmacen, getAlmacen, delArticulo, updateArticulo,updateArticuloCantidad } from "../funciones/almacen.js"
import { cors } from "../funciones/cors.js"
export default function handler(req, res) {
  cors(req, res)

  if (req.method === "POST") {

  
    if (parseInt(req.headers["id"]) === 0) {
      return addAlmacen(req, res)
    }
    if (parseInt(req.headers["id"]) === 1) {

      return delArticulo(req, res)
    }
    if (parseInt(req.headers["id"]) === 2) {
      return updateArticulo(req, res)
    }
    if (parseInt(req.headers["id"]) === 3) {
      return updateArticuloCantidad(req, res)
    }
  }
  console.log("qlkklk")
  return getAlmacen(req, res)

}