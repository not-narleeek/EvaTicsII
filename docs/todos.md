# To-Do PedioLink — camino a la entrega (lun 9-nov, 23:59)

Proyecto ficticio de nivel perfil: nada se "contrata" ni se "cotiza" — todo lo que no es real se **declara como supuesto y se justifica con una referencia de mercado citada** (la guía lo permite explícitamente: "libertad para hacer supuestos… que deben explicitar y justificar"). Cada ítem cerrado = comentario del docx resuelto o brecha de la verificación cubierta.

## P0 — Modelo económico consistente (bloquea Excel + caps. 17–19)

- [x] 1. Hoja `Supuestos` como única fuente de verdad: instituciones activas por año, precio (2.200 USD/mes), implementación (8k), cupo/estudios, churn, mezcla de ingresos
- [x] 2. Derivar ingresos año a año desde esos supuestos (corrige el ×10 del año 5)
- [x] 3. Reconstruir flujo de caja 5 años (Tabla 6) con costos consistentes con cap. 12 (486k/año, no 444k)
- [x] 4. Corregir CAPM: Ke = 14,9% con los insumos actuales, o ajustar insumos y citar la fila exacta de Damodaran (sector + fecha de la tabla)
- [x] 5. Recalcular VAN normal **y VAN ajustado** (pedido explícito), TIR, PRI simple y descontado, con fórmulas visibles en el Excel
- [x] 6. Escenarios pesimista/normal/optimista recalculados desde la nueva base; corregir "captura año 1: 3%" para que calce con el SOM
- [x] 7. Estado de resultados y balance 3 años con fila de control (Activo = Pasivo + Patrimonio), consistentes con el flujo
- [x] 8. Armar el Excel real: `Supuestos`, `Flujo de Caja`, `Estado Resultados`, `Balance`, `Evaluacion`, `Escenarios` (mismos nombres que cita el Word)

## P1 — Consistencia narrativa (decisión del 29-oct en TODO el cuerpo)

- [x] 9. ISP/Clase I: retirar de caps. 9 (Gantt), 10 (inversiones), 13 (legal), 19 (riesgos) **o** mantenerlo y justificarlo con fuente — decidir uno; si queda, conciliar M3-M6 vs. "≈6 meses"
- [x] 10. Leipzig → ZZU: reemplazar "Leipzig Heart Center"/"Leone et al." por el dataset ZZU (Tan et al., 2025, Scientific Data; cita completa en anexos/fuentes/bibliografia-por-capitulo.md) en FODA (cap. 6), solución técnica (cap. 8) y conclusión (cap. 20)
- [x] 11. Meta de 3 regiones (cap. 6: Valparaíso/Biobío) → reemplazar por criterios de expansión
- [x] 12. Kits IoT: eliminar de Gantt (actividad 5), bodega (caps. 7 y 15) y Ley REP (cap. 16) — el modelo declara "no incluye equipos"
- [x] 13. Alinear cap. 6 con el cliente declarado: quitar CESFAM/ISAPRE como canal año 1 o justificarlos; retirar "B2B2C probado" y toda precisión/utilidad presentada como demostrada
- [x] 14. Conclusión: eliminar o fundamentar "30 hospitales / 8.000 pacientes / un hospital por mes"; hacerla consistente con caps. 4–5
- [x] 15. SAM: fijar el conteo calificado (estimación declarada) para que SOM y escenarios sean proporcionales correctos

## P1 — Gráficos y diagramas (la guía los exige; hoy solo texto)

- [x] 16. CANVAS con código de color Propuesta de Valor ↔ Segmentos (#3)
- [x] 17. Diagrama BPMN de las 5 etapas descritas (cap. 7)
- [x] 18. Layout de oficina/bodega (cap. 7)
- [x] 19. Logo: imagen real del isotipo descrito (cap. 6) (#5)
- [x] 20. Gráficos de mercado: TAM-SAM-SOM y participación proyectada (#4)
- [x] 21. Organigrama en página apaisada legible (#20)
- [x] 22. Gantt: añadir especificidad (granularidad semanal, hitos) sobre la base actual (#9)
- [x] 23. Figura 4 regenerada: `informe/graficos/fig4_flujo.png` (insertar en el Word)

## P1 — Supuestos con referencia de mercado (ficticio ⇒ explicitar, no "cotizar")

- [ ] 24. Arriendo: referencia de mercado zona oriente (portal inmobiliario) citada; validar ≈0,53 UF/m² (#21, #22)
- [ ] 25. Cloud: estimación con AWS Pricing Calculator, captura a anexos, respaldar USD/estudio (#16)
- [ ] 26. Financiamiento: tasa vigente citada (BancoEstado), condiciones CORFO verificadas contra la convocatoria real; responder "por qué BancoEstado" con una condición concreta (#12, #15)
- [ ] 27. Inversiones y financiamiento en CLP/UF con tipo de cambio y fecha declarados (#11, #14) *(fila CLP lista en hoja `Flujo de Caja`; falta en el Word)*
- [ ] 28. Legal: fuente verificable para el registro de software (o reemplazar "Decreto Exento 25/2026"); explicitar Ley 21.719 y su entrada en vigencia (#18)
- [ ] 29. Reescribir pasajes "muy IA" en financiamiento y legal: decisiones directas, primera persona (#13, #17)

## P2 — Forma y entrega

- [x] 30. Bibliografía APA → `anexos/fuentes/bibliografia-por-capitulo.md` *(faltan solo fila/fecha de Damodaran)*
- [ ] 31. Portada: número de grupo e integrantes
- [ ] 32. TOC: actualizar campos antes de exportar a PDF
- [ ] 33. Enviar preguntas al profe ya: detalle del cap. 2 (#2), financiamiento (#12), ISP sí/no
- [ ] 34. PowerPoint + elevator pitch de 60 s (uno por integrante)
- [ ] 35. Anexos *(iniciado: `anexos/fuentes/bibliografia-por-capitulo.md`)* — agregar capturas PDF de las fuentes, cálculo AWS, referencias de arriendo
- [ ] 36. Ensayo de defensa: cada integrante domina todos los capítulos (80% de la nota es preguntas)

## Reparto sugerido (4 integrantes)

| Persona | Bloque | Ítems |
|---|---|---|
| A | Modelo económico + Excel | 1–8, 23 |
| B | Contenido caps. 4–8 + gráficos | 15–22, 25 |
| C | Legal, financiamiento, localización, supuestos | 9–14, 24, 26–29 |
| D | Forma, anexos, PPT, defensa | 30–36 |
