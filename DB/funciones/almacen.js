import { database } from "../module/db.js"
import path from "path"

export const addAlmacen = async (req, res) => {


    try {
        const cursor = await database()
        const data = req.body
        cursor.connection.run("INSERT INTO articulos(nombre,cantidad,precio,tipo) VALUES(?, ?, ?, ?)", data)
        res.json({ ok: true, res: "Artículo agregado correctamente" })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo agregar el artículo.", error: err })
    }
}
export const getAlmacen = async (req, res) => {



    try {
        const cursor = await database()
        const articulos = await cursor.connection.all("SELECT * FROM articulos")
        res.json({ ok: true, res: articulos })
    } catch (err) {
        console.log(err)


          res.json({ ok: false, res: "No se pudieron conseguir los artículos. ", error: err,path:path.resolve() })
    
    }
}
export const delArticulo = async (req, res) => {

    try {
        const cursor = await database()
        const data = req.body
        await cursor.connection.run("DELETE FROM articulos WHERE id=?", [data._id])
        res.json({ ok: true, res: "Artículo eliminado correctamente." })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo eliminar el artículo." })
    }

}
export const updateArticulo = async (req, res) => {

    try {
        const cursor = await database()
        const data = req.body
        await cursor.connection.run("UPDATE articulos set nombre=?, cantidad=?, precio=? where lower(nombre)=lower(?) ", data)
        res.json({ ok: true, res: "Artículo actualizado correctamente." })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo actualizar el artículo." })
    }

}

//UPDATE articulos SET cantidad = cantidad - ? WHERE id =? and cantidad > 0 and cantidad >= ? ",(item["cantidad"],item["ID"],item["cantidad"])
export const updateArticuloCantidad = async (req, res) => {

    try {
        const cursor = await database()
        const data = req.body
        await cursor.connection.run("UPDATE articulos SET cantidad = cantidad - ? WHERE id =? and cantidad > 0 and cantidad >= ? ",data)
        res.json({ ok: true, res: "Artículo actualizado correctamente." })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo actualizar el artículo." })
    }
}
