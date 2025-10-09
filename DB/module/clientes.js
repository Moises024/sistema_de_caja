import dataBase from "./db.js";
import mongoose from "mongoose";
import AutoIncrementFactory from 'mongoose-sequence';

let Clientes;

const getClienteModel = async () => {
  if (Clientes) return Clientes; // si ya está inicializado, lo devuelve

  const conn = await dataBase();
  const AutoIncrement = AutoIncrementFactory(mongoose);

  const clienteSchema = new mongoose.Schema({
    id: Number,
    nombre: { type: String, required: true },
    telefono: { type: String, required: true }
  });

  clienteSchema.plugin(AutoIncrement, { inc_field: 'id' });

  Clientes = conn.model("clientes", clienteSchema);
  return Clientes;
};

export default getClienteModel;
