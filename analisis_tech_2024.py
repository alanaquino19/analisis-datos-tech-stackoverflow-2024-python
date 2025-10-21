# Análisis de Datos: Encuesta Stack Overflow 2024.
# Genera gráficos y un informe PDF con resumen automático de las tecnologías más populares/usadas en el 2024.

import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# 1. Cargar CSV.
df = pd.read_csv("Encuesta Tech Stack Overflow 2024.csv")

# 2. Función para generar y guardar gráficos.
def plot_all(category):
    data = df[df['category'] == category].sort_values('usage_all', ascending=False)

    # 2.1. Color azul personalizado.
    azul = "#007BFF"
    colores = [azul for _ in range(len(data))]

    plt.figure(figsize=(7,6))
    plt.barh(data['technology'], data['usage_all'], color=colores, edgecolor="#0056b3")
    plt.gca().invert_yaxis()
    plt.xlabel("% de uso (todos)")
    plt.ylabel(category)
    plt.title(f"{category}: Todos los encuestados (Stack Overflow 2024)")
    plt.grid(axis="x", linestyle="--", alpha=0.4)
    filename = f"grafico_{category}.png"
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()
    return filename

# 3. Crear gráficos para todas las categorías.
categorias = df['category'].unique()
imagenes = [plot_all(cat) for cat in categorias]

# 4. Generar resumen automático.
def generar_resumen(df):
    resumen = []
    for cat in df['category'].unique():
        top = df[df['category']==cat].sort_values('usage_all', ascending=False).iloc[0]
        resumen.append(
            f"En la categoría {cat}, la tecnología más usada es {top['technology']} "
            f"con un {top['usage_all']}% de adopción entre todos los encuestados."
        )
    resumen.append(
        "\nEn general, las tecnologías más populares muestran estabilidad respecto a años anteriores, "
        "destacando JavaScript, PostgreSQL, Docker y React como líderes en sus respectivas áreas."
    )
    return "\n".join(resumen)

resumen_texto = generar_resumen(df)

# 5. Crear informe PDF.
def generar_pdf(nombre_pdf, imagenes, resumen_texto):
    doc = SimpleDocTemplate(nombre_pdf, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph("Análisis de Tecnologías Stack Overflow 2024", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Informe generado automáticamente con Python y matplotlib.", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("<b>Resumen General:</b>", styles['Heading2']))
    story.append(Paragraph(resumen_texto.replace("\n", "<br/>"), styles['Normal']))
    story.append(Spacer(1, 0.4*inch))

    for img_path in imagenes:
        story.append(Spacer(1, 0.3*inch))
        story.append(Image(img_path, width=6*inch, height=4*inch))
        story.append(Spacer(1, 0.2*inch))

    doc.build(story)
    print(f"Informe generado correctamente: {nombre_pdf}")

# 6. Ejecutar todo.
generar_pdf("Informe Stack Overflow 2024.pdf", imagenes, resumen_texto)