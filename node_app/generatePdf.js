const puppeteer = require('puppeteer');

async function generatePDF(url, outputPath) {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'networkidle0' });
        const pdfPath = outputPath;
        const pdfOptions = {
            path: pdfPath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '5mm',
                bottom: '5mm',
                left: '5mm',
                right: '5mm'
            }
        };
        await page.pdf(pdfOptions);

        await browser.close();
        console.log(`PDF gerado com sucesso! Salvo em: ${pdfPath}`);
    } catch (error) {
        console.error('Erro ao gerar PDF:', error);
    }
}

const url = process.argv[2]; // process.argv[2] é o primeiro argumento real passado ao script
const outputPath = process.argv[3] || 'output.pdf'; // Caminho do arquivo, default 'output.pdf'
generatePDF(url, outputPath);