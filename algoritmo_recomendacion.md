## 1. Cálculo de la puntuación de una oferta (`calcular_puntuacion_oferta`)

Esta función devuelve un **número entre 0 y 120** que mide lo atractiva que es una oferta para un usuario concreto. Se compone de seis bloques:

1. **Coincidencia de habilidades (hasta 40 pts)**

   * Se toman como conjuntos las habilidades del usuario y las requeridas por la oferta.
   * Se calcula el porcentaje de habilidades requeridas que el usuario posee:

     $$
       \text{porcentaje\_match} = \frac{\lvert H_{\text{usuario}} \cap H_{\text{oferta}}\rvert}{\lvert H_{\text{oferta}}\rvert}.
     $$
   * Se añade a la puntuación hasta 40 pts:

     $$
       \min\bigl(40,\;40 \times \text{porcentaje\_match}\bigr).
     $$

2. **Nivel de experiencia (hasta 20 pts)**

   * Se mapean niveles `{junior:1, intermedio:2, senior:3}`.
   * Se evalúa la diferencia absoluta entre nivel del usuario y nivel de la oferta:

     * 0 niveles de diferencia → +20 pts
     * 1 nivel → +10 pts
     * ≥2 niveles → +5 pts

3. **Ubicación y modalidad (hasta 25 pts)**

   * **Ubicación (15 pts)**

     * Misma ciudad → +15 pts
     * Misma región (mismo primer segmento antes de la coma) → +10 pts
     * Mismo país (mismo último segmento) → +5 pts
   * **Modalidad (10 pts)**

     * Coincide exactamente “presencial”/“remoto” → +10 pts
     * Cualquiera de ellos es “mixto” → +5 pts

4. **Nivel académico (hasta 15 pts)**

   * Se mapean niveles académicos `{ninguno:1, secundaria:2, técnico:3, universitario:4, posgrado:5}`.
   * Si el usuario cumple o supera el nivel requerido → +15 pts
   * Si se queda justo un nivel por debajo → +7 pts

5. **Multiplicador por antigüedad de la oferta**

   * Se calcula cuántos días han pasado desde la creación:

     * ≤ 1 día → × 1.2
     * ≤ 3 días → × 1.1
     * ≤ 7 días → × 1.0
     * ≤ 14 días → × 0.9
     * ≤ 30 días → × 0.8
     * > 30 días → × 0.7

6. **Bonificaciones y penalizaciones**

   * **Bonificaciones** (máximo +8 pts por “likes” y +7 pts por vistas):

     * Cuenta cuántas ofertas de esa misma industria el usuario ha “likeado”:
       `min(8, likes_similares * 2)`.
     * Cuenta cuántas veces ha visto ofertas de esa industria ≥ 30 s:
       `min(7, vistas_similares)`.
   * **Penalizaciones**:

     * Si ya se postuló a **esa** oferta → −20 pts.
     * Si tiene > 10 postulaciones activas en los últimos 30 días → −10 pts.
     * Si tiene entre 6 y 10 postulaciones activas → −5 pts.

Al final se **limita** la puntuación al rango \[0, 120].

---

## 2. Generación de recomendaciones (`generar_recomendaciones_usuario`)

1. **Contar postulaciones activas**
   Postulaciones del usuario en los últimos 30 días → `postulaciones_activas`.

2. **Filtrar ofertas**

   * Se obtienen todas las ofertas en la base de datos.
   * Se excluyen las que el usuario ya ha postulado (para no repetir).

3. **Calcular y ordenar**

   * Para cada oferta disponible, se llama a `calcular_puntuacion_oferta(...)`.
   * Se guarda la tupla `(oferta, puntuación)`.
   * Se ordena de mayor a menor puntuación.

4. **Devolver top N**

   * Se toman los primeros `limit` (por defecto 10) y se devuelven sólo las instancias de oferta.

---
