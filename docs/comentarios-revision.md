# Comentarios de revisión — PedioLink_Informe_PEP(1).docx

Extraídos de `word/comments.xml` el 2-nov-2026 (30 comentarios, 19-oct a 29-oct). "Ancla" = texto del informe sobre el que está el comentario. Autores anónimos salvo el #1 (D. Iturra, 29-oct, que define los cambios acordados para la introducción).

## Decisiones ya acordadas (comentario #1, aplicar en TODO el cuerpo)

> **Ancla:** Introducción — *Los cambios principales son:*
> - Objetivos centrados en evaluar el proyecto, en lugar de dar por decidida su comercialización.
> - Retiro del ISP y de la clasificación "Clase I": el marco regulatorio deberá verificarse en el apartado legal.
> - Eliminación de las tres regiones como meta arbitraria: se proponen criterios para evaluar una expansión.
> - Retiro del dataset Leipzig, sin sustituirlo por otra base todavía no validada.
> - Separación entre propuesta y resultados demostrados: ya no se presenta la precisión o utilidad clínica como algo comprobado.

**Estado:** la introducción ya fue editada en esa línea, pero el cuerpo AÚN contiene: ISP/Clase I (caps. 9, 10, 13, 19), Leipzig (caps. 6, 8, 20), expansión a 3 regiones (cap. 6), precisión 95%/Brier 0,2 (cap. 8). → Barrido pendiente.

## Por capítulo

### Cap. 1 — Introducción
- **#0** (ancla: *Introducción*): "A parte de las modificaciones sugeridas en comentarios, revisar cómo hacer una Introducción para este tipo de proyectos y adaptar. Si tuviera que evaluar esta introducción es 2/5" *(19-oct; previo a la reedición del 29-oct)*

### Cap. 2 — Definición del Proyecto
- **#2** (ancla: *Definición del Proyecto*): "Preguntas para el Profe: 1. Este apartado es necesario una descripción exhaustiva y técnica de todo?, ejemplo de lo que me refiero: si indicamos que es un SaaS, se debe indicar qué compañía de servidores contrataremos?, la arquitectura que utilizaremos para lanzar y mantener el producto funcionando?"

### Cap. 3 — Modelo de Negocios (CANVAS)
- **#3** (ancla: *Canvas*): "Falta color coded: Propuesta de Valor_Segmentos del Mercado"

### Cap. 5 — Situación de Mercado
- **#4** (ancla: *Situación de Mercado*): "Faltan graficos"

### Cap. 6 — Plan / Estrategia Comercial
- **#5** (ancla: *Plan / Estrategia Comercial*): "FODA pobre, no hay PEST, no hay logo"

### Cap. 8 — Solución Técnica Requerida
- **#8** (ancla: *cifrado TLS 1.3 en tránsito*): "Revisar"
- **#6** (ancla: *se transmite al servidor de PedioLink mediante HTTPS o HL7*): "Definir"
- **#7** (ancla: *clasificación supervisada mediante Random Forest o SVM … dataset Leipzig Heart Center*): "modificar"
- **#29** (ancla: *dataset Leipzig*): "No"

### Cap. 9 — Carta Gantt-PERT
- **#9** (ancla: *Figura 2. Carta Gantt*): "Tomar la fig. Como base, pero se debe mejorar añadiendo especificidad."
- **#10** (ancla: *la compra de kits IoT de capacitación*): "Por qué deberíamos comprar kits IoT."

### Cap. 10 — Inversiones Necesarias
- **#11** (ancla: *Inversiones Necesarias*): "Añadiría su precio en CLP, teniendo encuenta inflación o algo, IDK, CPL_UTM_UF o algo."

### Cap. 11 — Financiamiento
- **#12** (ancla: *Financiamiento*): "Este apartado es bastante débil y debe ser desarrollado más, idealmente debemos consultar a nuestro profe para feedback."
- **#13** (ancla: *prácticas habituales de startups HealthTech en Chile*): "Muy I.A"
- **#14** (ancla: *Estructura de financiamiento del proyecto*): "Precio CLP o equivalente en Chile."
- **#15** (ancla: *BancoEstado*): "Por qué este banco?"

### Cap. 12 — Costos Estimados
- **#16** (ancla: *Costos Estimados*): "Considero que falta especificidad, ejemplo incluir cotizaciones, colocar referencias de empresas reales."

### Cap. 13 — Aspectos Legales
- **#17** (ancla: *La justificación de esta elección frente a las alternativas … se basa en cuatro razones*): "La manera de presentar esto es muy I.A, al nostros definir una SPA solo debemos explicar porque."
- **#18** (ancla: *Agencia Nacional de Protección de Datos*): "Aún que la agencia no está establecida aún (y no lo estará en un tiempo próximo), veo importante también incluir explicitamente la ley de protección de datos."

### Cap. 14 — Aspectos del Personal
- **#19** (ancla: *Aspectos del Personal Necesario*): "Debemos indicar si hacemos outsourcing the alguna área?."
- **#20** (ancla: *organigrama*): "El organigrama no se vé, será mejor dejar una pág en blanco para este y colocarlo de manera horizontal."

### Cap. 15 — Localización
- **#21** (ancla: *una oficina de 100 m² más una bodega anexa de 50 m²*): "Buscaría oficinas reales en la zona para startup y usaría su información como referencia real."
- **#22** (ancla: *el valor del arriendo de USD 2.500 mensuales por 150 m² …*): "Alguna cita que valide nuestras afirmaciones."

### Cap. 16 — Aspectos Ambientales
- **#23** (ancla: *…reciclaje de los kits electrónicos entregados a hospitales…*): "Hell no." *(contradice el modelo SaaS sin hardware; eliminar o reescribir)*

### Cap. 17 — Flujo Proyectado y EEFF
- **#24** (ancla: *Tabla 6. Flujo de Caja proyectado*): "Literal revisar esto y hasta hacerlo desde cero."
- **#25** (ancla: *La proyección muestra que el proyecto alcanza el punto de equilibrio…*): "Verificar que la jerga usada haya sido enseñada en clases, y no estemos invadiendo mucho el territorio de los comerciales qls."

### Cap. 18 — Evaluación
- **#26** (ancla: *Evaluación (TIR, VAN, Payback, CAPM)*): "No tengo ni idea de si está bueno o no, hay que revisarlo desde cero." *(la revisión confirma errores: ver verificacion-cumplimiento.md, cap. 18)*

### Cap. 19 — Sensibilización
- **#27** (ancla: *Sensibilización del Proyecto*): "Nuevamente ni idea, probablemente hacer desde cero."

### Cap. 20 — Conclusión
- **#28** (ancla: *El proyecto PedioLink combina cuatro elementos…*): "Faltan citas apropiadas"

*(30 comentarios: IDs 0–29, todos listados.)*
