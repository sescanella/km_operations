from pydantic import BaseModel
from typing import List, Optional

class Material(BaseModel):
    mat_descripcion: str
    mat_dn: str
    mat_sch: str
    mat_qty: int
    mat_numero_interno: Optional[str] = None

class Joint(BaseModel):
    union_numero: str
    union_dn: str
    union_tipo: str
    union_armador: Optional[str] = None
    union_soldador_raiz: Optional[str] = None
    union_soldador_remate: Optional[str] = None

class Spool(BaseModel):
    spool: str
    materials: List[Material]
    joints: List[Joint]

class Plan(BaseModel):
    plano: str
    spool_data: Spool

class SaleNote(BaseModel):
    nv: str
    plans: List[Plan]
