import { database } from "../module/db.js"
export const addInventario = async (req,res)=>{
    const cursor = await database()
    const data = req.body

    try {
        cursor.connection.run("INSERT INTO facturas(usuario_id,factura,total,fecha) VALUES(?, ?, ?, ?) ",data)
        res.json({ok:true,res:"Factura agregada correctamente."})
    } catch (error) {
         res.json({ok:true,res:"No se pudo agregar dicha factura.",error})
    }
}
export const getInventario = async (req,res)=>{
    const cursor = await database()
    try {
       const data = await  cursor.connection.all("SELECT * FROM facturas JOIN usuarios ON usuarios.id = facturas.usuario_id order by facturas.fecha desc")
        res.json({ok:true,res:data})
    } catch (error) {
         res.json({ok:true,res:"No se pudo agregar dicha factura.",error})
    }
}
 export const delInventario = async (req, res) => {
   
    const cursor = await database()
    const data = req.body
    try {
        cursor.connection.run("DELETE FROM facturas WHERE id=?",[data._id])
        res.json({ ok: true, res: "Artículo eliminado correctamente" })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo eliminar el artículo.", error: err })
    }
}