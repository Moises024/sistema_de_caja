import getAlmacenModel from "../module/almacen.js"
import path from "path"

export const addAlmacen = async (req, res) => {

   
    try {
        const Almacen = await getAlmacenModel()
        const data = req.body
        const data_almacen = {
            nombre:data[0],
            cantidad:data[1],
            precio:data[2]
        }
        const articulo = await new Almacen(data_almacen)
        await articulo.save()
        
        res.json({ ok: true, res: "Artículo agregado correctamente" })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo agregar el artículo.", error: err })
    }
}
export const getAlmacen = async (req, res) => {
    try {
        const Almacen = await getAlmacenModel()
        const articulos = await Almacen.find({}).sort({id:-1})
        res.json({ ok: true, res: articulos })
    } catch (err) {
        console.log(err)
        res.json({ ok: false, res: "No se pudieron conseguir los artículos. ", error: err,path:path.resolve() })
    }
}
export const delArticulo = async (req, res) => {

    try {
         const Almacen = await getAlmacenModel()
        const data = req.body
        await Almacen.findOneAndDelete({id:data._id})
        res.json({ ok: true, res: "Artículo eliminado correctamente." })
    } catch (err) {
        console.log(err)
        res.json({ ok: false, res: "No se pudo eliminar el artículo." })
    }

}
export const updateArticulo = async (req, res) => {

    try {
  
        const data = req.body
        const Almacen = await getAlmacenModel()
        await Almacen.updateOne({nombre:data[0]},{$set:{
            precio:data[2],
            cantidad:data[1]
        }})
        res.json({ ok: true, res: "Artículo actualizado correctamente." })
    } catch (err) {
        res.json({ ok: false, res: "No se pudo actualizar el artículo." })
    }

}

//UPDATE articulos SET cantidad = cantidad - ? WHERE id =? and cantidad > 0 and cantidad >= ? ",(item["cantidad"],item["ID"],item["cantidad"])
export const updateArticuloCantidad = async (req, res) => {

    try {
        
        const data = req.body
       
        console.log(data,"Actualidzar un ncantadiad")
       
        const Almacen = await getAlmacenModel()
       
        const update = await Almacen.updateOne({id:data[1]},{$inc:{cantidad:-data[0]}})
        
        console.log(update)
        res.json({ ok: true, res: "Artículo actualizado correctamente." })
    } catch (err) {
        res.json({ ok: false, res: `"No se pudo actualizar el artículo." ${err}` })
    }
}
