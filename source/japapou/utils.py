import qrcode
from io import BytesIO
import uuid
import base64

def gerar_pix_simulado(order_id, total):
    '''Gera um código PIX (chave de pagamento) e um QR Code em Base64 simulados.'''

    chave_simulada = (
        f"3002br.gov.bcb.pix01"
        f"22{str(order_id).zfill(5)}{str(total).replace('.', '')}"
        f"{str(uuid.uuid4()).replace('-', '')[:16]}52040000530398654"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(chave_simulada)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return chave_simulada, qr_code_base64