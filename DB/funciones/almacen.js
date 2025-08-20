import { database } from "../module/db.js"
export const addAlmacen = async (req, res) => {
   
    const cursor = await database()
    const data = req.body
    try {
        cursor.connection.run("INSERT INTO articulos(nombre,cantidad,precio,tipo) VALUES(?, ?, ?, ?)", data)
        res.json({ ok: true, res: "Artículo agregado correctamente" })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo agregar el artículo.", error: err })
    }
}
export const getAlmacen = async (req, res) => {
    
    const cursor = await database()
   
    try {
       const articulos  = await cursor.connection.all("SELECT * FROM articulos")
        res.json({ ok: true, res: articulos })
    } catch (err) {
        res.json({ ok: false, res: "No se pudieron conseguir los artículos. ", error: err })
    }
}
export const delArticulo = async (req,res)=>{
     const cursor = await database()
     const data = req.body
     try{
        cursor.connection.run("DELETE FROM articulos WHERE id=?",[data._id])
        res.json({ok:true,res:"Artículo eliminado correctamente."})
     }catch(err){
        res.json({ok:false,res:"No se pudo eliminar el artículo."})
     }

}
