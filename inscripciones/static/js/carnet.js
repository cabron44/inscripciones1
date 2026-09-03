document.addEventListener('DOMContentLoaded', () => {
    const shareButton = document.getElementById('share-carnet');
    const carnetId = shareButton ? shareButton.dataset.carnetId : '';

    const downloadImage = (blob) => {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `carnet_${carnetId}.png`;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
    };

    if (!shareButton) {
        return;
    }

    shareButton.addEventListener('click', () => {
        const element = document.querySelector('.card');

        html2canvas(element, {
            scale: 2,
            useCORS: true
        }).then((canvas) => {
            canvas.toBlob((blob) => {
                if (!blob) {
                    return;
                }

                const file = new File([blob], `carnet_${carnetId}.png`, { type: 'image/png' });
                const canShareFiles = typeof navigator.canShare === 'function'
                    && navigator.canShare({ files: [file] });
                if (navigator.share && canShareFiles) {
                    navigator.share({
                        title: 'Carnet de Alumno',
                        text: 'Carnet generado desde el sistema de inscripciones.',
                        files: [file]
                    }).catch(() => downloadImage(blob));
                } else {
                    downloadImage(blob);
                    alert('Tu navegador no soporta compartir archivos. La imagen se descargará automáticamente.');
                }
            });
        }).catch(() => {
            alert('Error al generar la imagen del carnet.');
        });
    });
});
