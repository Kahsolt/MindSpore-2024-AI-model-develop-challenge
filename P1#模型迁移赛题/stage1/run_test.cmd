SET RUN_SLOW=1
(√)

================================================================================================================================================================================================

[wav2vec2_bert] 【完成！】
pylint --rcfile=.github/pylint.conf tests\ut\transformers\models\wav2vec2_bert
pytest -v -s tests\ut\transformers\models\wav2vec2_bert (√)

================================================================================================================================================================================================

[FastSpeech-Conformer] 【完成！】
pylint --rcfile=.github/pylint.conf tests\ut\transformers\models\fastspeech2_conformer (√)
pytest -v -s -c pytest.ini tests\ut\transformers\models\fastspeech2_conformer (√)

pytest -v -s tests\ut\transformers\models\fastspeech2_conformer\test_tokenization_fastspeech2_conformer.py (√)
pytest -v -s tests\ut\transformers\models\fastspeech2_conformer\test_modeling_fastspeech2_conformer.py (√)

================================================================================================================================================================================================

[Mask2Former]
pylint --rcfile=.github/pylint.conf mindnlp\transformers\models\swin (√)
pylint --rcfile=.github/pylint.conf mindnlp\transformers\models\mask2former (√)
pylint --rcfile=.github/pylint.conf tests\ut\transformers\models\mask2former (√)

pytest -v -s tests\ut\transformers\models\mask2former\test_image_processing_mask2former.py (√)
pytest -v -s tests\ut\transformers\models\mask2former\test_modeling_mask2former.py (1)
pytest -v -s tests\ut\transformers\models\mask2former\test_modeling_mask2former.py::Mask2FormerModelTest (1)
pytest -v -s tests\ut\transformers\models\mask2former\test_modeling_mask2former.py::Mask2FormerModelTest::test_initialization
pytest -v -s tests\ut\transformers\models\mask2former\test_modeling_mask2former.py::Mask2FormerModelIntegrationTest (√)

================================================================================================================================================================================================

[OneFormer]
pylint --rcfile=.github/pylint.conf mindnlp\transformers\models\oneformer (√)
pylint --rcfile=.github/pylint.conf tests\ut\transformers\models\oneformer (√)

pytest -v -s tests\ut\transformers\models\oneformer\test_image_processing_oneformer.py (√)
pytest -v -s tests\ut\transformers\models\oneformer\test_processor_oneformer.py (√)
pytest -v -s tests\ut\transformers\models\oneformer\test_modeling_oneformer.py (1)
pytest -v -s tests\ut\transformers\models\oneformer\test_modeling_oneformer.py::OneFormerModelTest::test_initialization

================================================================================================================================================================================================

[DeTR]
pylint --rcfile=.github/pylint.conf mindnlp\transformers\models\detr (√)
pylint --rcfile=.github/pylint.conf tests\ut\transformers\models\detr (√)

pytest -v -s tests\ut\transformers\models\detr\test_image_processing_detr.py (√)
pytest -v -s tests\ut\transformers\models\detr\test_modeling_detr.py (√)

FAILED tests\ut\transformers\models\detr\test_modeling_detr.py::DetrModelTest::test_save_load_fast_init_from_base - AssertionError: 84672.0 not less than or equal to 0.001 : model.backbone.conv_encoder.model.embedder.embedder.convolution.weight not ide...

[DeTR-hf]
pytest -v -s tests\models\detr\test_modeling_detr.py::DetrModelIntegrationTests::test_inference_no_head
