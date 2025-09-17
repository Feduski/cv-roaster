import PyPDF2
from docx import Document
import io

class PDFProcessor:
    @staticmethod
    async def extract_text_from_file(file_content: bytes, filename: str) -> str:
        """
        Extrae texto de un archivo PDF o DOCX desde memoria
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo para determinar el tipo
        Returns:
            str: Texto extraído del archivo
        """
        try:
            # Determinar tipo de archivo por extensión
            if filename.lower().endswith('.pdf'):
                return await PDFProcessor._extract_from_pdf(file_content)
            elif filename.lower().endswith(('.doc', '.docx')):
                return await PDFProcessor._extract_from_docx(file_content)
            else:
                raise ValueError("Formato de archivo no soportado")
                
        except Exception as e:
            raise Exception(f"Error procesando archivo: {str(e)}")

    @staticmethod
    async def _extract_from_pdf(file_content: bytes) -> str:
        """Extrae texto de un PDF en memoria"""
        try:

            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            #leer cada página
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            text = PDFProcessor._clean_text(text)
            
            if not text.strip():
                raise Exception("No se pudo extraer texto del PDF")
            return text
            
        except Exception as e:
            raise Exception(f"Error procesando PDF: {str(e)}")

    @staticmethod
    async def _extract_from_docx(file_content: bytes) -> str:
        """Extrae texto de un DOCX en memoria"""
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            text = PDFProcessor._clean_text(text)
            
            if not text.strip():
                raise Exception("No se pudo extraer texto del DOCX")    
            return text
            
        except Exception as e:
            raise Exception(f"Error procesando DOCX: {str(e)}")

    @staticmethod
    def _clean_text(text: str) -> str:
        """Limpia y normaliza el texto extraído"""
        # Remover espacios extra y líneas vacías
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)

    @staticmethod
    def validate_file_size(file_content: bytes, max_size_mb: int = 5) -> bool:
        """Valida que el archivo no sea muy grande"""
        size_mb = len(file_content) / (1024 * 1024)
        return size_mb <= max_size_mb