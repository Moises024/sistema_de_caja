import getClienteModel from "../module/Clientes.js"
export const setCliente = async (req,res)=>{
    const data = req.body
    const new_cliente = {
        nombre: data[0],
        telefono :data[1]
    }
    const Cliente = await getClienteModel()
    const cliente = await new Cliente(new_cliente)
    await cliente.save()
    res.json({ok:true,res:cliente._id})
}   

export const getCliente = async (req,res)=>{
    
    const Cliente = await getClienteModel()
    const cliente = await Cliente.find({})
    res.json({ok:true,res:cliente})
}

export const updateCliente = async ()=>{

}