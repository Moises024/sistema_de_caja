import dataBase from "./db.js";
import mongoose from "mongoose";
import AutoIncrementFactory from 'mongoose-sequence';

let Usuario;

const getUsuarioModel = async () => {
  if (Usuario) return Usuario; // si ya está inicializado, lo devuelve

  const conn = await dataBase();
  const AutoIncrement = AutoIncrementFactory(mongoose);

  const usuarioSchema = new mongoose.Schema({
    id: Number,
    nombre: { type: String, required: true },
    apellido: { type: String, required: true },
    contra: { type: String, required: true },
    rol: { type: Number, default: 1 },
    usuario: { type: String, required: true },
  });

  usuarioSchema.plugin(AutoIncrement, { inc_field: 'id' });

  Usuario = conn.model("usuarios", usuarioSchema);
  return Usuario;
};

export default getUsuarioModel;
