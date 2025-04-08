Para utilizar este repositorio, es necesario activar el entorno de Monai, donde se instalarán todas las librerías necesario.
En la consola, ejecutamos: .\nombre_de_tu_carpeta\Scripts\python.exe
Una vez ejecutado, tendremos que activarlo: .\nombre_de_tu_carpeta\Scripts\activate  o si estás en GitBash: source nombre_de_tu_carpeta/Scripts/activate
Una vez dentro, ejecutaremos el siguiente comando para instalar todas las dependencias: pip install -r requirements.txt
requirements.txt se encuentra en la ruta de nuestro proyecto

Para utilizar el modelo preentrenado de lung nodule de MODEL ZOO, tenemos que clonar el repositorio: https://github.com/Project-MONAI/model-zoo/tree/dev/models/lung_nodule_ct_detection  y copiar el archivo model.pt en la ruta de nuestro proyecto




