import argparse
from onmt.utils.logging import init_logger
from onmt.translate.translator import build_translator
import onmt.inputters
import onmt.translate
import onmt
import onmt.model_builder
import onmt.modules
import onmt.opts

def translate():
    parser = argparse.ArgumentParser(description='nmt_translator.py',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    onmt.opts.add_md_help_argument(parser)
    onmt.opts.translate_opts(parser)
    default_opts = [
        '-model', 'trans_en_fr.pt',
        '-src', 'cache/src.txt',
        '-output', 'cache/pred.txt',
        '-replace_unk',
        '-verbose'
    ]
    opt = parser.parse_args(default_opts)

    translator = build_translator(opt, report_score=True)
    translator.translate(src_path=opt.src,
                         tgt_path=opt.tgt,
                         src_dir=opt.src_dir,
                         batch_size=opt.batch_size,
                         attn_debug=opt.attn_debug
                         )
