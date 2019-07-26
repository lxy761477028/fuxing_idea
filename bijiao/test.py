
def test(convert):
    if convert == True:
        convertForm(predict_filename.replace('.csv', '_check_result.csv'),
                    predict_filename.replace('.csv', '_check_result.xlsx'))
        convertForm(bianzhu_filename.replace('.csv', '_check_result.csv'),
                    bianzhu_filename.replace('.csv', '_check_result.xlsx'))
        try:
            os.remove(bianzhu_filename.replace('.csv', '_check_result.csv'))
            os.remove(predict_filename.replace('.csv', '_check_result.csv'))
        except:
            True
    else:
        print("haha")

test(convert = False)